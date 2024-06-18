using System;
using System.IO;
using Microsoft.Extensions.Logging;
using IdsLib;
using IdsLib.IdsSchema.IdsNodes;
using Serilog;
using Serilog.Extensions.Logging;
using static IdsLib.Audit;

class Program
{
    static void Main()
    {
        // Specify the absolute path for the log file
        string logFilePath = @"C:\Users\ivanf\Downloads\log.txt";

        // Configure Serilog
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Information()
            .WriteTo.Console(outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss} [{Level}] {Message}{NewLine}{Exception}")
            .WriteTo.File(logFilePath, outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss} [{Level}] {Message}{NewLine}{Exception}")
            .CreateLogger();

        // Create LoggerFactory using Serilog
        using var loggerFactory = LoggerFactory.Create(builder =>
        {
            builder
                .AddFilter("idsTool.Program", LogLevel.Information)
                .AddSerilog();
        });

        Microsoft.Extensions.Logging.ILogger logger = loggerFactory.CreateLogger<Program>();

        // Correct the file path
        string filePath = @"C:\Users\ivanf\Downloads\hola.ids";

        // Create a stream for the IDS file
        using (FileStream idsStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
        {
            // Create and configure an instance of SingleAuditOptions
            SingleAuditOptions options = new SingleAuditOptions
            {
                IdsVersion = IdsVersion.Ids0_9_7 // Set the appropriate version of the schema
            };

            // Call the Audit.Run method
            Status result = Audit.Run(idsStream, options, logger);
            // Log the audit result
            logger.LogInformation($"Audit result: {result}");
            // display the audit result in console
            Console.WriteLine($"Audit result: {result}");
        }
    }
}
