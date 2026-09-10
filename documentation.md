# Computer Game Development: From Idea to Implementation
## Tips (Pitfalls, What I Stepped On)
Please don't skip this if you want to avoid the pitfalls described here
### AI Is an Assistant, Not a Replacement for a Developer
Using AI is possible and necessary, but with wisdom
- **License risk**: AI may generate code protected by copyright (for example, under copyleft licenses such as [GNU GPL](https://www.gnu.org/licenses/gpl-3.0.en.html). If you plan to keep your code closed-source, this will violate the law.
- **Learning**: Blind copy-pasting deprives you of understanding. It's better to spend time learning and writing the logic yourself, and based on the knowledge gained, be able to solve dozens of typical tasks, than to search for an error in yet another generated, incomprehensible piece of code.

Remember: AI is a tool, it should help you, not do everything for you
#### What Is AI Actually Useful For?
- Automating routine tasks (writing boilerplate code, if you understand how it works)
- Error checking
- New ways to solve a problem
### Verify Resources
Everything you take from public sources (textures, sound, models, code, etc.) has its own license. Make sure the author allows free use
### Don't Rush
You will manage everything, the result may not be quick. Rushing can lead to numerous errors that may require rewriting all the code from scratch
### Protect Yourself from Burnout
Working through force is the main enemy of indie projects. If you feel that the project irritates you — take a pause for as long as needed.
It's better to take a pause than to abandon the project forever.
### Think First, Then Do
Before writing and implementing something new, sketch out a plan. There is almost always a more elegant way to implement a specific mechanic.
## Idea and MVP Prototype
There are many genres and directions. Determine which one you want to implement and create a game model:
- **Analysis of analogues**: look at existing analogues
- **Implementation**: study the implementation of similar mechanics, determine the initial functionality

## Choosing Development Tools
Decide on your technology stack:
- ### Programming Language
Choose the options you're comfortable writing in and for which there are plenty of learning materials and a community.

**Popular options**:
- [C#](https://docs.microsoft.com/en-us/dotnet/csharp/) — the standard for [Unity](https://unity.com)
- [C++](https://isocpp.org/) with [Unreal Engine](https://unrealengine.com)
- [Python](https://www.python.org/) with [PyGame](https://www.pygame.org/docs)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript) for browser games
- ### Integrated Development Environment (IDE)
The environment where you'll write code. It should be convenient (or highly customizable), highlight errors, and have autocomplete.

**Popular options**:
- [VS Code](https://visualstudio.com)
- [VSCodium](https://vscodium.com) (same as VSCode, without Microsoft telemetry)
- [PyCharm](https://jetbrains.com) (for Python, JavaScript)
- [Neovim](https://neovim.io) — the ultimate tool for [GNU/Linux](https://www.gnu.org/gnu/linux-and-gnu.html) systems, but you need to install plugins to turn it into a comfortable IDE
- ### Game Engine
It takes care of the routine: rendering, physics calculations, and sound processing
- **Ready-made engines**:
- - [Unity](https://unity.com)
- - [Unreal Engine](https://unrealengine.com)
- - [Godot](https://godotengine.org)
- **Your own**: for those who want to understand how rendering and math work from the inside. It's written in pure code based on technical literature. **_Downside_**: instead of creating a game, you'll spend months writing code that just displays an image on the screen. For an MVP project, it's better to take a ready-made one.
- ### Working with Graphics and Sound
You'll need programs for creating or editing assets
- **2D graphics**: [Photoshop](https://photoshop.adobe.com), [GIMP](https://gimp.org), [Aseprite](https://aseprite.org) (ideal for pixel art).
- **3D modeling**: [Blender](https://blender.org)
- **Sound**: [Audacity](https://audacityteam.org), [Reaper](https://reaper.fm).
## Game Architecture
A regular program (like a calculator) waits for user action and freezes. You can't do that with a game — the world must live even if the player takes their hands off the keyboard. For this, there is a game loop — an infinite loop. Each iteration of the loop consists of three steps:

1. Input handling — process user keystrokes
2. Update — taking into account user actions, move characters, calculate physics, check collisions
3. Render — output the finished image to the screen

It's impossible to write a universal step-by-step guide after this stage, because game genres, languages, and engines differ too much from each other.

This guide was created to help beginners avoid the main pitfalls at the start of developing their first (or next) MVP project and to understand the general logic of gamedev. I hope the information here was useful!