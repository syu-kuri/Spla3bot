<div align="center"><img src="docs/img/logo.png" width="400"/></div>

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
@Spla3Bot 現在のナワバリ
```
**Slash Command**
```
/現在のナワバリ
```
**Command**
```
!次のナワバリ
```

## List of commands
### View current stage information
* `現在のナワバリ` ... Returns the current Navavari stage information.
* `現在のバンカラチャレンジ` ... Returns the stage information of the current challenge match
* `現在のバンカラオープン` ... Returns stage information for the current open match
### View next stage information by relative specification
* `次のナワバリ` ... Returns stage information for the next Navarari
* `次のバンカラチャレンジ` ... Returns stage information for the next challenge match
* `次のバンカラオープン` ... Returns stage information for the next open match
### View stage information for the next 24 hours from the current stage
* `すべてのナワバリ` ... Returns the stage information of the next Navarry for the next 24 hours
* `すべてのバンカラチャレンジ` ... Returns stage information for the next challenge match up to 24 hours in the future
* `すべてのバンカラオープン` ... Returns stage information for open matches up to 24 hours in the future

## Example of command execution
<div align="center"><img src="docs/img/example.png" width="400"/></div>

## Future Progress
* ~~Support for Salmon Run information after API support~~
* Search for specific rules
* Search for specific time
* Support for shortened command search
