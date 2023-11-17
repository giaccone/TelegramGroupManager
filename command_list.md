# Available commands

## admin commands

| admin command                    | notes                                    |
|----------------------------------|------------------------------------------|
| `/autokick reason`               | answering to the user message            |
| `/autoban reason`                | answering to the user message            |
| `/ban reason`                    | answering to the user message (reason can be ommitted)            |
| `/ban user_id reason`            | standalone message (reason can be ommitted)                       |
| `/ban username reason`           | standalone message (reason can be ommitted)                       |
| `/unban`                         | answering to the user message            |
| `/unban user_id`                 | standalone message                        |
| `/unban username`                | standalone message                        |
| `/kick reason`                   | answering to the user message (reason can be ommitted)            |
| `/kick user_id reason`           | standalone message (reason can be ommitted)                       |
| `/kick username reason`          | standalone message (reason can be ommitted)                       |
| `/mute`                          | answering to the user message            |
| `/unmute`                        | answering to the user message            |
| `/pin`                           | answering to the message to be pinned    |
| `/slow flag n_mex seconds`       | read footnote [1]                        |
| `/log`                           |                                          |


[1] meaning of the `\slow` parameters:
* `flag`:
    * 0: deactivate
    * 1: activate
* `n_mex`: max allowed consecutive number of messages
* `seconds`: seconds muted if `n+1` consecutive messages are sent


## user commands

These commands are not very useful. They are implemented only for completeness.

| user command                     | notes         |
|----------------------------------|---------------|
| `/start`                         |               |
| `/help`                          |               |
    
