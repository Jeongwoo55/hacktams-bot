require('dotenv').config(); 

const fs = require('fs');
const Discord = require('discord.js');
const { prefix } = require('../config.json');

const client = new Discord.Client();
client.commands = new Discord.Collection();

client.once('ready', () => {
    console.log('Ready!');
});

client.login(process.env.DISCORD_BOT_TOKEN);


const commandFiles = fs.readdirSync('src/commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.name, command);
}

client.on('message', message => {
    if (!message.content.startsWith(prefix) || message.author.bot) return;

    const args = message.content.slice(prefix.length).trim().split(/ +/);
    const command = args.shift().toLowerCase();

    if (!client.commands.has(command)) return;

    try {
        client.commands.get(command).execute(message, args);
    } catch (error) {
        console.error(error);
        message.reply('there was an error trying to execute that command!');
    }

})




client.on('voiceStateUpdate', (oldMember, newMember) => {
    let newUserChannel = newMember.voice.channel
    let oldUserChannel = oldMember.voice.channel


    if (oldUserChannel === undefined && newUserChannel !== undefined) {

        console.log('something happened ö')
        if (newMember.id == 688237618835619897) {
            const connection = newUserChannel.join();
            const dispatcher = connection.play(ytdl('https://www.youtube.com/watch?v=4GnVDPD01as'));
        }


    } else if (newUserChannel === undefined) {

        // User leaves a voice channel

    }
})


