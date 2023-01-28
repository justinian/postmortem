# POST mortem

This is a little utility to put together an [Exquisite Corpse][1] poem for the
[Taskmaster][2]-inspired _Amandatory 2023_.

[1]: https://en.wikipedia.org/wiki/Exquisite_corpse
[2]: https://en.wikipedia.org/wiki/Taskmaster_(TV_series)

## The task

> _Post Mortem_
>
> Create an Exquisite Corpse poem.
> Begin a poem then mail your unfinished work to another person.
> Have that person add to the poem & mail to another person etc... Each recipient
> must add to the poem. YOUR POEM MUST BE 25 WORDS.
>
> You will present your poem at AMANDATORY 2023.
>
> Points are awarded for greatest distance traveled via post. A bonus point will be
> awarded for best poem.
>
> You have until AMANDATORY 2023 (_date redacted_) to complete this task.
>
> Your time starts now.

## The plan

While "via post" is more often used in British English, it's still likely to be
understood to mean "by mail" in American English. However, that's not the
_only_ thing it could mean. To software engineers, "via post" can also mean
"using the HTTP `POST` verb".

Interpreting "post" as `POST`, and the verb "mail" to refer to electronic mail,
it's reasonable to interpret emailing links to a web application as adhering to
the letter of the task.

Thus this little app allows a group of people to collaboratively add to a poem,
copying it and a URL to add to it for emailing to the next person.

## The distance

Thanks to the magic of public cloud providers and SSH tunnels, I've set up a
server for the app in Seattle, and SSH jump hosts in Sydney and Tokyo. A
reverse proxy runs on the same machine as the proxy, but points at the app via
an SSH tunnel routed through the two jump hosts. (See OpenSSH's `ProxyJump`
configuration, or the `-J` command-line option.) If every user adding to the
poem is connecting from the San Francisco Bay Area, the total distance the
`POST` travels from browser to app is 29,132 km.

I squeeze further distance out of this setup by making the front-end need to
send a `POST` for every word and every newline added to the poem.
