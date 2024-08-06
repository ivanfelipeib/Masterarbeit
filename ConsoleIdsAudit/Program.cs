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
        // Determine the root directory of the project
        string baseDirectory = AppContext.BaseDirectory;
        string rootFolder = Path.Combine(baseDirectory,".."); //navigate up to root directory
        rootFolder= Path.GetFullPath(rootFolder);
        
        // Specify the relative paths for the log file and IDS file
        string logFilePath = Path.Combine(rootFolder, "temp_files", "log.txt");
        string filePath = Path.Combine(rootFolder, "temp_files", "TempIds.ids");

        // Check if log file exists; if not, create it. If file exists clear log
        if (!File.Exists(logFilePath))
        {
            File.WriteAllText(logFilePath, string.Empty);
        }
        else
        {
            File.WriteAllText(logFilePath, string.Empty);
        }

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

        // Check if the IDS file exists; if not, throw an exception
        if (!File.Exists(filePath))
        {
            string errorMessage = "The IDS file 'TempIds.ids' does not exist.";
            logger.LogError(errorMessage);
            Console.WriteLine(errorMessage);
            throw new FileNotFoundException(errorMessage);
        }
        
        // Create a stream for the IDS file
        using (FileStream idsStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
        {
            // Create and configure an instance of SingleAuditOptions
            SingleAuditOptions options = new SingleAuditOptions
            {
                //IDS Version is not automatically recognized must be given according to enum IdsVersion from IDSAuditTool
                IdsVersion = IdsVersion.Ids0_9_7 // Set the appropriate version of the schema
            };

            // Call the Audit.Run method
            Status result = Audit.Run(idsStream, options, logger);
            // Log the audit result
            logger.LogInformation($"Audit result: {result}");
            // Display the audit result in console
            Console.WriteLine($"Audit result: {result}");
        }
    }
}
