---
title: "Human Verification Architecture Proposal"
date: "2025-07-28"
draft: true
tags: 
- software engineering
- architecture
- programming
- security engineering
- AI technology
---

Problem: LLM's make it impossible to know what content is human generated. I do not wish to spend time reading blogs, articles, and tweets that are not human generated. 

Solution: A trusted domain signs written content that is verified via some heurisitic mechanism to have been written without the aid of technology for content. 

Constraints: 
- verification service does not store any content or hash; simple attestation service only 
- users can include a "human-generated" stamp on their published content, allowing any user to check that the content was written by a human. 

# High level Architecture

Mobile application using Google Play Integrity API or iOS App Attestation. Unfortunately, authenticity of web apps cannot be reliably verified in the way that mobile apps can. 

Mobile app implements some heuristics like key counting to attempt to verify that the content was written by a human. 

When ready, the client submits content for verification stamp. 

Backend, verifying the application authenticity, signs the content if verified. Returns 200 OK to the client. 

User can then publish the content anywhere, along with the verification stamp. The stamp would be some linked image which directs a verification page with the signature encoded in the URL. The verification page waits for the verifier to paste the plaintext content and click verify. This sends the content and signature to the backend where it is hashed and checked against the signature. If the decrypted signature and the content hash match, 200 is returned to the client. 

