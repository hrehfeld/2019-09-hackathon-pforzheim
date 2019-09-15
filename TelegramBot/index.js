const Telegraf = require("telegraf");
const request = require("request-promise");
const bot = new Telegraf("986773128:AAFPYbyxIE99-f22x0zH-sEXcFCigNp6k7A");
const analyzeImgEndpoint = "http://localhost:5000";

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
    const b64 = await getImageFileAsB64(fileId);
    //console.log(b64);
    ctx.reply("Verarbeitung...");
    const productInfo = await getProductInfo(b64);
    handleProductInfoReceived(ctx, productInfo);
}

async function handleDocument(ctx) {
    const fileId = ctx.message.document.file_id;
    const b64 = await getImageFileAsB64(fileId);
    //console.log(b64);
    ctx.reply("Verarbeitung...");
    const productInfo = await getProductInfo(b64);
    handleProductInfoReceived(ctx, productInfo);
}

function defaultHandler(ctx) {
    ctx.reply("Bitte sende mir ein Foto.");
}

async function getImageFileAsB64(fileId) {
    const fileLink = await bot.telegram.getFileLink(fileId);
    console.log(fileLink); 
    const buffer = await getImageFileAsBuffer(fileLink);
    return buffer.toString('base64');
}

async function getImageFileAsBuffer(url) {
    const body = await request.get(url, { encoding: null });
    return new Buffer(body);
}

async function getProductInfo(base64Img) {
    const body = JSON.stringify({ base64: base64Img });
    const result = await request.post(analyzeImgEndpoint, {
        body: body,
        headers: {
            "content-type": "application/json"
        }
    })
    .catch(err => {
        console.error(err);
        return {
            success: false
        }
    });
    try {
        return JSON.parse(result);
    }
    catch(err) {
        return {
            "success": false
        };
    }

}

async function handleProductInfoReceived(ctx, result) {
    console.log(result);
    if(result.success == true) {
        const productImg = await getImageFileAsBuffer(result.img);
        const price = result.price;
        const name = result.name;
        const description = result.desc;
        ctx.replyWithPhoto({source: productImg}, {caption: result.name});
        ctx.reply("Preis: " + price);
        ctx.reply("Beschreibung: " + description);
        ctx.reply("Willst du dieses Produkt bestellen?");
    } else {
        ctx.reply("Das Bild konnte leider nicht erkannt werden, bitte versuche es erneut.")
    }
}

