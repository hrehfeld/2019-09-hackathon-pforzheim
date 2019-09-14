using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Net.Http;
using System.Net;
using System.Text.RegularExpressions;
using System.Net.Http.Formatting;
using System.Linq;

namespace TextProcessing
{
    public static class TextProcessing
    {
        [FunctionName("TextProcessing")]
        public static async Task<HttpResponseMessage> Run(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)] HttpRequest req, ILogger log)
        {
            var obj = JsonConvert.DeserializeObject<Result>(await req.ReadAsStringAsync());
            var response = new HttpResponseMessage(HttpStatusCode.BadRequest);

            if (obj.IsSuccess())
            {
                response.StatusCode = HttpStatusCode.OK;
                var responseObjects = new List<Response>();

                foreach (var line in obj.RecognitionResult.Lines)
                {
                    var lineText = line.Text.Trim().Replace(" ", "").Replace("/", "");

                    var isArticle = IsArticleNumber(lineText);
                    if (isArticle.Success)
                    {
                        responseObjects.Add(new Response
                        {
                            ArticleNumber = isArticle.Value
                        });
                    }
                    else
                    {
                        var isSize = IsSizeNumber(lineText);
                        if (string.IsNullOrEmpty(responseObjects.Last().SizeNumber) && isSize.Success)
                        {
                            responseObjects.Last().SizeNumber = isSize.Value;
                        }
                    }
                }

                response.Content = new ObjectContent<object>(responseObjects, new JsonMediaTypeFormatter(), "application/json");
                return response;

            }

            return response;
        }

        public static Match IsArticleNumber(string text)
        {
            return Regex.Match(text, "([0-9]{6})");
        }

        public static Match IsSizeNumber(string text)
        {
            return Regex.Match(text, "([1]?[0-9]{1,2})");
        }
    }

    public class Response
    {
        [JsonProperty("articleNumber"), JsonRequired]
        public string ArticleNumber { get; set; }
        [JsonProperty("sizeNumber")]
        public string SizeNumber { get; set; }
    }

    public class Result
    {
        public string Status { get; set; }
        public RecognitionResult RecognitionResult { get; set; }

        public bool IsSuccess() => Status == "Succeeded";
    }

    public class RecognitionResult
    {
        public IList<Line> Lines { get; set; }
    }

    public class Line
    {
        public IList<string> BoundingBox { get; set; }
        public string Text { get; set; }
        public IList<object> Words { get; set; }
    }
}