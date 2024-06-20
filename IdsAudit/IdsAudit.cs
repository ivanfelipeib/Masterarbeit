using System;
using System.IO;
using Microsoft.Extensions.Logging;
using IdsLib;
using IdsLib.IdsSchema.IdsNodes;
using Serilog;
using Serilog.Extensions.Logging;
using static IdsLib.Audit;

namespace IdsAuditLib
{
    public class IdsAudit
    {
        public static string RunAudit(string filePath, string idsVersionStr)
        {
            //parse input text in Enum type
            if (!Enum.TryParse(idsVersionStr, out IdsVersion idsVersion))
            {
                return "Invalid IDS Version";
            }

            // Specify the absolute path for the log file
            string logFilePath = @"C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\BIMQA_Quick_Checker\temp_files\log.txt";

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
                    .AddFilter("IdsAuditLib.IdsAudit", LogLevel.Information)
                    .AddSerilog();
            });

            Microsoft.Extensions.Logging.ILogger logger = loggerFactory.CreateLogger<IdsAudit>();

            // Create a stream for the IDS file
            using (FileStream idsStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                // Create and configure an instance of SingleAuditOptions
                SingleAuditOptions options = new SingleAuditOptions
                {
                    IdsVersion = idsVersion // Set the appropriate version of the schema
                };

                // Call the Audit.Run method
                Status result = Audit.Run(idsStream, options, logger);
                // Log the audit result
                logger.LogInformation($"Audit result: {result}");
                // Return the audit result
                return $"Audit result: {result}";
            }
        }
    }
}
