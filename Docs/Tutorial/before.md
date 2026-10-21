# Before You Begin

Welcome! We will build a small Markdown notebook together.

You do not need to understand the whole application yet.
Let's make one small change, check it, and then move on.

By the end, you will be able to:

- Convert Markdown into HTML.
- Sign in and save your own notes.
- Upload a picture and restore a deleted note.
- Translate the interface and run the app in Docker.

## How to use this tutorial

Read the chapters in order.
Each chapter starts where the previous one stopped.

Run **one command at a time**.
Wait for it to finish before running the next command.

Text labelled **Expected** describes the result. Do not type that text.

At a **checkpoint**, pause and try the listed actions.
If a check fails, stay in that chapter. Later steps depend on it.

## Three places we will work

**Terminal:** where you type commands such as `dotnet build`.

**Editor:** where you open and change source files.

**Browser:** where you try the running application.

The terminal's current folder matters.
`pwd` prints that folder. `cd` changes it.

We will create the project at `~/Source/MyOrg.MarkToHtml`.
We call that folder the **repository root**.

Paths beginning with `src/` are relative to that root.
Do not create another `src` folder inside the web project.

## Start and stop the app

A running web server keeps its terminal busy. That is normal.

When we ask you to stop the app, click its terminal and press **Ctrl+C**.
Wait until the command prompt returns.

Then you can edit the files and run the next command in that same terminal.
This also prevents two copies of the app from trying to use port 5000.

## A few gentle guardrails

Keep the files Voyager generates.
We will point out exactly where to add our own code.

A **complete file** block replaces that file.
An **insert** block goes inside an existing file at the named location.
We will distinguish them before you copy.

The database and uploaded files are real data.
Only reset your own disposable tutorial data. Leave other applications alone.

This tutorial uses .NET 10, Node.js 24, and the current Voyager template.
Installation and downloads can take a while. There is no time limit.

Ready? Let's [create the project](./step1.md).
