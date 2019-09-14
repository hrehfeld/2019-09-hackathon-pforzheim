const Telegraf = require("telegraf");
const request = require("request-promise");
const bot = new Telegraf("986773128:AAFPYbyxIE99-f22x0zH-sEXcFCigNp6k7A");

bot.start(ctx => ctx.reply("Hallo! Bitte schicke mir ein Foto mit Artikeln, die du im Katalog markiert hast."));
bot.on("message", async (ctx) => {
    if (ctx.message.photo) {
        return await handlePhoto(ctx);
    } else if (ctx.message.document) {
        return await handleDocument(ctx);
    } else {
        return defaultHandler(ctx);
    }
});

bot.launch();

async function handlePhoto(ctx) {
    const fileId = ctx.message.photo[ctx.message.photo.length - 1].file_id;
    await getImageFile(fileId);
    ctx.reply("OK Photo");
}

async function handleDocument(ctx) {
    const fileId = ctx.message.document.file_id;
    await getImageFile(fileId);
    ctx.reply("OK Document");
}

function defaultHandler(ctx) {
    ctx.reply("Bitte sende mir ein Foto.");
}

async function getImageFile(fileId) {
    const fileLink = await bot.telegram.getFileLink(fileId);
    console.log(fileLink);
    request.get(fileLink)
        .then(data => console.log("got data"))
        .catch(err => console.error(err));
}

