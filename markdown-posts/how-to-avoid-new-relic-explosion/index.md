---
title: "How to Avoid New Relic Metric Explosion"
date: "2018-09-13"
draft: true
tags:
- new relic
- observability
- software engineering
- medium article
---


SafetyCulture we use New Relic to monitor most of our services. It has been hugely valuable to our company by enabling quick analysis of massive data sets in near real-time. New Relic is a regular source of actionable insights; for example, the iAuditor API team recently leveraged the New Relic dashboard to adjust rate limits for an expanding customer base.

This article describes how to avoid one of the common pitfalls experienced by users of New Relic. That is, a Metric Grouping Issue (MGI) or “metric explosion” as it’s often referred to.

![](https://img.tonycodes.com/explosion.webp)

## When does an MGI occur?
An MGI occurs when a service sends many unique individual metrics that would be better managed in groups. This presents a challenge for New Relic as it can slow down their overall user experience. Additionally, this can overwhelm the dashboard insights making it difficult to identify problem spots. One way to identify if an MGI is occurring is if “you are seeing “/*” in your transaction names.”[1] If the issue persists, New Relic will take action to halt accounts from creating any additional metric names for the offending service if an MGI is occurring.

One example of a situation with the potential for an unbounded number of metric names to cause MGI is from an edge service like the iAuditor API. This service exposes a number of iAuditor resources each identified by a universally unique identifier (UUID).

New Relic does a great job of automatically grouping transactions. However, in the case of the HapiJS framework used by the iAuditor API, the automatic grouping is done once a request enters the route handler. In certain cases, like a validation error, the route handler is never entered. In this case the metric is not automatically grouped, instead, it is sent to the New Relic API as a raw URL string. Since this includes UUID information it is guaranteed to be unique. With a large user base experimenting with the iAuditor API validation errors are commonplace. The result was a metric explosion, or MGI.

## How did we solve it?
To solve this problem, we implemented custom naming rules to replace automatic metric naming. Custom naming rules take precedence over automatic naming and are applied to the URL path rather than the name returned by the router instrumentation. The rule can be stored as an environment variable or New Relic configuration file.

For example, take a common request handled by the iAuditor API, Update Response Set. The request URL is in the format,

```
https://api.safetyculture.io/response_sets/responseset_7db5002c72754d2a99ac1e4b82f088be/responses/64285441-782f-4891-b0f7-2beffbdd78bc
```

https://api.safetyculture.io/response_sets/responseset_7db5002c72754d2a99ac1e4b82f088be/responses/64285441-782f-4891-b0f7-2beffbdd78bc
When this request succeeds New Relic automatically groups the request as,

```
https://api.safetyculture.io/response_sets/{response set}/responses/{response ID}
```

https://api.safetyculture.io/response_sets/{response set}/responses/{response ID}
However, in the case of the Hapi JS framework, if the request causes a validation error then the raw URL is sent to New Relic as a unique metric name which contributes to an MGI.

Here is the custom naming rule we set up to handle the iAuditor Response Set API:

```bash
NEW_RELIC_NAMING_RULES = '{"pattern": "^\/response_sets\/.*","name": "/response_sets/"}'
```


The pattern can be a regular expression or string. In this case, any incoming URL that matches the pattern will be grouped as /response_sets/. The naming rules can be set via an environment variable (as shown above) or the New Relic configuration file. See the README here [2] for more information about setting metric naming rules.

### New Relic Transaction List before & after custom metric naming:

![](https://img.tonycodes.com/new-relic-insights.webp)

Note that this is not the only way an MGI can occur. Validation errors are only the cause in the specific experience of the iAuditor API team. According to New Relic, MGI can also occur in the following scenarios:

- If your application is crawling the Internet and each external call goes to a different domain
- If your software dynamically generates temporary database tables every time you receive a request
- If you are using custom instrumentation that includes UUIDs, article names, or similar unique components [3]

Custom metric naming is a way to safeguard against most causes of an MGI.

Many modern languages make it straightforward to work with HTTP and create custom strategies for naming and routing requests for services like RESTful APIs. However, the URLs are often not the ideal grouping for performance monitoring. Use custom naming rules to avoid an MGI, keep New Relic unblocked, and ensure reliable monitoring.

---

# References
- [Relic Solution: Why Are My Transactions Named /*!, New Relic Web site](https://discuss.newrelic.com/t/relic-solution-why-are-my-transactions-named/41737). New Relic. Retrieved 28 August 2018.
- [newrelic/node-newrelic](https://github.com/newrelic/node-newrelic), New Relic Github repository. New Relic. Retrieved 28 August 2018.
- [Metric grouping issue](https://docs.newrelic.com/docs/agents/manage-apm-agents/troubleshooting/metric-grouping-issues), New Relic Web site. New Relic. Retrieved 27 August 2018.

Originally published on [Medium](https://medium.com/safetycultureengineering/how-to-avoid-new-relic-metric-explosion-301615cf2af1)
