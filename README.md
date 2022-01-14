# Vert-CLI
A CLI made with Typer.

**Sintaxis:** ```vert <app> <command> [arg]```

By default, your persistence is in JSON, not in PostgreSQL

## User guide
In Linux, for a better experience, type ```sudo nano .zshrc``` in the last line:
```
alias vert='~/path/to/vert-cli'
```
Later: ```source .zshrc```

![Alt Text](https://media.giphy.com/media/OHi0W7hGDwmI8ejPyP/giphy.gif)

Once this is done, you can enjoy it just typing ***vert --help***
<br>This will drop to you a list of commands as:

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Commands:
  categories
  core
  gen
  ideas
  notifier
  tables
  tasks
  urls

```

Well, look the options of one command, like ```vert core --help```

![Alt Text](https://media.giphy.com/media/lHVG4ds0Rtzy5GP0wi/giphy.gif)

Comes the most underrated part, type ```vert core version```
<br>
***Congratulations!*** 🎉, you just have to explore the other commands in the other applications.

## Configurations

### PostgreSQL and Workspace configuration
 - Type ```vert core config``` to configure you database connection and workspace path
 - Then ```vert core change-persistence```
 - Finally to build the tables in your database: ```vert tables rebuild```
 
![Alt Text](https://media.giphy.com/media/e7VOxIUHJA7QRJy7a6/giphy.gif)

###  Workspace
You know what I'm talking about, the placement where your projects are, give me an absolute path as ```~/workspace/projects```

```
vert core workspace-config
```

### PostgreSQL
The option for a better performance

 - Type ```vert core db-config``` to set your settings, previously you need to create an PSQL database
 - Later ```vert core change-persistence``` and select ***PostgreSQL***.
 - To build your tables in your database, type ```vert tables rebuild```
 

## License
MIT License

Copyright (c) 2022 Luis Quiñones Requelme

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

