<div align="center"><img src="../docs/img/logo.png" width="400"/></div>

# Discord Bot for Splatoon 3
<p align="center">
  <a href="//github.com/syu-kuri/Spla3bot/releases"><img src="https://img.shields.io/github/v/release/syu-kuri/Spla3bot"></a>
  <a href="//github.com/syu-kuri/Spla3bot/issues"><img src="https://img.shields.io/github/issues-raw/syu-kuri/Spla3bot"></a>
  <a href="//github.com/syu-kuri/Spla3bot/releases"><img src="https://img.shields.io/github/downloads/syu-kuri/Spla3bot/total"></a>
  <a href="//github.com/syu-kuri/Spla3bot/commits/main"><img src="https://img.shields.io/github/last-commit/syu-kuri/Spla3bot"></a>
  <a href="//github.com/syu-kuri/Spla3bot"><img src="https://img.shields.io/github/languages/code-size/syu-kuri/Spla3bot"></a>
</p>


This is a Discord Bot that returns Splatoon 3 stage information by either Mention, Slash Command, or Command.

This bot uses the API of [Spla3 API](https://spla3.yuu26.com/) produced by Emuon to get information.

## Invite Discord server
[Click here to invite Spla3bot to your server](https://discord.com/api/oauth2/authorize?client_id=1020415520337576066&permissions=2147503104&scope=bot%20applications.commands)

## Reports and Requests
Please report bugs and requests for additional features to [Discord Server](https://discord.gg/zwbvUPTZHc) or to an issue in this repository.


## How to use the command
**Mention**
```
@Spla3Bot regular now
```
**Slash Command**
```
/regular now
```
**Command**
```
!regular now
```

## List of commands
### View current stage information
* `regular now` ... Returns the current Navavari stage information.
* `challenge now` ... Returns the stage information of the current challenge match
* `open now` ... Returns stage information for the current open match
* `coop now` ... Returns the current Salmon Run stage and buki information
### View next stage information by relative specification
* `regular next` ... Returns stage information for the next Navarari
* `challenge next` ... Returns stage information for the next challenge match
* `open next` ... Returns stage information for the next open match
* `coop next` ... Returns stage and buki information for the next Salmon Run
### View stage information for the next 24 hours from the current stage
* `regular all` ... Return stage information for up to 12 Navarari
* `challenge all` ... Returns stage information for up to 12 challenge matches
* `open all` ... Returns stage information for up to 12 open matches
* `coop all` ... Returns up to 12 Salmon Run stages and buki information

## Example of command execution
<div align="center"><img src="docs/img/example1.png" width="400"/></div>

## Future Progress
* ~~Support for Salmon Run information after API support~~
* Search for specific rules
* Search for specific time
* Support for shortened command search
