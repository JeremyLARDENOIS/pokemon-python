<h1 align="center"><code>pokemon-python</code></h1>

<p align="center">
	<a href="https://GitHub.com/JeremyLARDENOIS/pokemon-python/graphs/commit-activity"><img src="https://img.shields.io/badge/maintained%3F-yes-green.svg"></a> <!--Maintained?-->
	<a href="https://GitHub.com/JeremyLARDENOIS"><img src="https://img.shields.io/badge/maintainer-JeremyLARDENOIS-red"></a> <!--Maintainer-->
	<a href="https://GitHub.com/JeremyLARDENOIS/pokemon-python/issues"><img src="https://img.shields.io/github/issues/JeremyLARDENOIS/pokemon-python.svg"></a> <!--Issues-->
	<a href="https://github.com/JeremyLARDENOIS/pokemon-python/stargazers"><img src="https://img.shields.io/github/stars/JeremyLARDENOIS/pokemon-python"/></a> <!--Stars-->
</p>

<h2 align="center">A simple, online, round-by-round combat platform.</h2>

---

## Simple functionality

You can use `pokepy_server.py` to create a server and `pokepy.py` to join an existing server.

## With parameters

Default IP is localhost and default port is 3333. You can change this setting on the server and client using the CLI.

Example for server:

```sh
./pokepy_server.py --host 127.0.0.2 --port 1234
```

Equivalent example for client:

```sh
./pokepy.py --host 127.0.0.2 --port 1234
```

## What's the purpose?

This project was initially a project I made to enter into an Engineer school, and it worked!

It's based on Pokemon and the game of Roshambo (AKA Rock-Paper-Scissors or Shi-Fu-Mi), where each attack does damage based on the attack of the opponent.

## Build and launch the server with docker

```sh
docker build -t pokepy .
docker run -p 3333:3333 -d pokepy
```

## Test of lint (with pylint)

```sh
pylint pokepy_server.py
pylint pokepy.py
```

## Test of type (with mypy)

```sh
mypy pokepy_server.py pokepy.py
```

## To Do

- Verify functionality on Windows and MacOS
- Create a `Tkinter` or web interface
- Create a system of levelling up
- Create a system of Player-versus-AI (look dev branch)
- Make sure that `pokepy_server.py` doesn't crash if clients crash
- Send a message to one client if the other crash
- Create a loop to re-ask for a response if the client's input is invalid, or if they take too long to answer
- Upgrade network protocol or use another library/framework
- Make a multi-platform server (several combat instances at the same time)
- Alert the client if the server crashes
- Record the user's network protocol
- Implement tests
- Implement defense/armor caracteristics
- Create differents class of player RPG based
- Close socket when `pokepy_server.py` crash except if mode restart always
- Verify user entry: add "choice" network verb that allow to only choose between some option 
- Make git pre-hooks mypy, pylint and explain how to use it in Readme
- Add Redis database
- Separate skills in a class
- Separate networks stuff in a module
- Make a refactor for client and server lib
- i18n
- Refactor `lib/server.py` and `lib/client.py`

## Bug Reports and Contributions

Don't hesitate to create Issues or Pull Request if you want to contribute to this project, ask questions, or just give feedback. Enjoy!

## Crédits

Main coder: [JérémyLARDENOIS](https://github.com/JeremyLARDENOIS)

Beautify and correct errors in README: [TurnipGuy30](https://github.com/TurnipGuy30)

<!--
  ~ README upgraded by @TurnipGuy30 ~ Find me at GitHub.com/TurnipGuy30 ~
-->
