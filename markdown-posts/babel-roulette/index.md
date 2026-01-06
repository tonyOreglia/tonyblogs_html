---
title: "Babel Roulette"
date: "2021-03-30"
draft: false
tags:
- language learning
- web development
- WebRTC
- Socket.io
- projects
---

## The Difficulty with Learning a New Language

In my opinion, the most useful method by far when it comes to learning a new language is (maybe not surprisingly) speaking with native speakers. The more often the better.

However, this is not always easy. For some, it's not comfortable striking up conversations with strangers. It's not a lot of fun stumbling through a basic sentence while your hostage tutor waits. Plus, often times the conversations is short lived; not providing much of an opportunity to practice.

Furthermore, in many places english is a second language. In some cases the language learner is constantly missing opportunities to learn as people switch to english for convenience.

Of course, there are websites that fill this need. For example, [Conversation Exchange](https://conversationexchange.com/) provides a platform to connect with language partners, whom you can have a conversation with in your target language, and teach your native language to. But still, there is some friction here - it require messaging a bunch people and scheduling a date/time to meet. It takes a lot of time to schedule, and often times the language partner doesn't even show up in the end. It's a free service so the commitment level is low.

I started to wish there was a platform offering immediate connectivity with other language learners out there. Remember chat roulette from the late 90's? I had in mind this kind of instant connectivity. It could have a settings to filter your partners for the language you are learning.

With this vision in mind, I built "Babel Roulette"; where a person can go and immediately be connected to other users speaking their target language.

## Babel Roulette

Babel Roulette is in it's it's initial Minimum Viable Product release. Currently the following rooms exists

* Visit the Portuguese speaking chat room at https://tonycodes.com/babelroulette/pt

* Visit the Spanish speaking chat room at https://tonycodes.com/babelroulette/es

* Visit the Italian speaking chat room at https://tonycodes.com/babelroulette/it

* Visit the English speaking chat room at https://tonycodes.com/babelroulette/en

You can also create a personal chat room by visiting https://tonycodes.com/babelroulette/. You will be forwarded to a private chat room. Share the full link with whomever you would like to chat with.

If you want to try it out, I will be online for english conversations at https://tonycodes.com/babelroulette/en Thursdays 6 - 6:20 PM Lisbon Time (GMT+1)
and at https://tonycodes.com/babelroulette/pt para ter conversas em português de 6:20 - 6:40 PM.

## Technical Details

### Tech Stack

* [Javascript](https://www.javascript.com/): The EcmaScript implementation we all love

* [EJS](https://ejs.co/): Embedded JavaScript templating

* [Express](https://expressjs.com/): Express is a minimal and flexible Node.js web application framework. It's used here to configure the server.

* [PeerJS](https://peerjs.com/): PeerJS wraps the browser's WebRTC implementation to provide an easy-to-use peer-to-peer connection API. This app uses PeerJS to easily create a P2P video stream connection to a remote peer.

* [WebRTC](https://webrtc.org/): a free, open-source project providing real-time communication (RTC) via simple application programming interfaces (APIs).

* [Socket.io](https://socket.io/): Socket.IO is a library that enables real-time, bidirectional and event-based communication between the browser and the server. At it's simplest, it's a nice websocket wrapper. It's used here to allow the client to join shared rooms handled on the server side.

* [React](https://reactjs.org/)

* [Material Design](https://material.io/design): Material is a design philosophy / system created by Google

### Building Babel Roulette

Building a video application is really about using the right tools for the job. If you review the code; you'll see it's a very light application. This is largely due to [WEbRTC](https://webrtc.org/) which performs signal processing, codec handling, peer-to-peer communication, security and bandwidth management; it allows bidirectional communication between peers with low latency. Using the PeerJS wrapper for creating a peer-to-peer video connection the implementation is even lighter.

One difficulty is how to implement the concept of separate rooms. This logic is handled on the server side where the various users connected to the applications can be grouped up by room ID. This is where [Socket.io](https://socket.io/) is very useful. Each client links up to the server at instantiation with a persistent socket.io connection. The room ID is embedded in the URL. For example, if you visit `https://tonycodes.com/babelroulette/en` your are joining the `en` room; `en` is your room ID in this case.

Socket.io has a great feature that implements the concept of a room. So each user that visits `babelroulette/en` is added to the socket.io `en` room on the server side. Socket.io allows a message to be broadcast to all members in that room. So each time a new member joins the room, a message a broadcast to all existing members. Then, on the browser side, PeerJS is used to create a new peer-to-peer connection with each member that received the broadcast connection.

Socket.io receiving an attempt to join a room looks like this and broadcasting this out looks like:

```js
// 'join-room' event sent from client
socket.on("join-room", (roomId, peerJsUserId) => {
  // Adds the socket to the given room
  // A Room is a server-side concept that allows broadcasting data to a subset of clients
  socket.join(roomId);
  // 'broadcast' sets a modifier for a subsequent event emission that the event data will only be broadcast to every sockets but the sender.
  // emit user-connected event
  socket.to(roomId).broadcast.emit("user-connected", peerJsUserId);

  socket.on("disconnect", () => {
    socket.to(roomId).broadcast.emit("user-disconnected", peerJsUserId);
  });
});
```

Note that PeerJS works via unique user IDs. This user ID is sent to the server via socket.io (as shown above) and broadcast out to all members of the room (also via socket.io). Then the unique peerJS user ID is used by PeerJS to call the new member and setup a video stream connection.

In the case of a user visiting `https://tonycodes.com/babelroulette/` in which case a new room ID is generated; EJS makes it easy to pass the room ID to the client with this snippet within the static EJS file:

```html
<script>
  const ROOM_ID = "<%= roomId %>";
</script>
```

This can be passed to the client from the server side with:

```js
app.get("/:room", (req, res) => {
  res.render("room", { roomId: req.params.room });
});
```

Note that `app` is an instance of an [Express](https://expressjs.com/) application. This is created with `const app = express();`

**[Check out Babel Roulette source code here!](https://github.com/tonyOreglia/babel-roulette)**

## Final Thoughts

Ultimately, I would like to see an application where each user can earn credits by speaking in their native language with others learning that language. Then those credits can be "spent" learning from native speakers in your target language.
`Teach and Earn` or `Learn and Burn`

Babel Roulette is a proof of concept to show how this type of application can be built. I learned a lot building it, had a lot of fun, and proved to myself that an application of this sort is completely within reach.