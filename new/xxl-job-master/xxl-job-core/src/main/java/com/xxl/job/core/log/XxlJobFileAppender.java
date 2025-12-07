package com.xxl.job.core.log;

import com.xxl.job.core.openapi.model.LogResult;
import com.xxl.tool.core.DateTool;
import com.xxl.tool.core.StringTool;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Date;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * store trigger log to console
 *
 * @author xuxueli 2016-3-12 19:25:12
 */
public class XxlJobFileAppender {
	private static final Logger logger = LoggerFactory.getLogger(XxlJobFileAppender.class);

	private static final ConcurrentHashMap<String, ConcurrentLinkedQueue<String>> logCache = new ConcurrentHashMap<>();

	public static void initLogPath(String logPath) {
		logger.info("Console logging mode: log path parameter ignored");
	}

	public static String getLogPath() {
		return "console";
	}

	public static String getGlueSrcPath() {
		return "console/gluesource";
	}

	public static String getCallbackLogPath() {
		return "console/callbacklogs";
	}

	/**
	 * log identifier
	 *
	 * @param logId log id
	 * @return log identifier
	 */
	public static String makeLogFileName(Date triggerDate, long logId) {
		return DateTool.formatDate(triggerDate) + "/" + logId;
	}

	/**
	 * append log to console
	 *
	 * @param logFileName log identifier
	 * @param appendLog   append log
	 */
	public static void appendLog(String logFileName, String appendLog) {

		// valid
		if (StringTool.isBlank(logFileName) || appendLog == null) {
			return;
		}

		// log to console
		logger.info("[{}] {}", logFileName, appendLog);

		// cache for readLog
		logCache.computeIfAbsent(logFileName, k -> new ConcurrentLinkedQueue<>()).add(appendLog);
	}

	/**
	 * support read log from cache
	 *
	 * @param logFileName log identifier
	 * @param fromLineNum from line num
	 * @return log content
	 */
	public static LogResult readLog(String logFileName, final int fromLineNum) {

		// valid
		if (StringTool.isBlank(logFileName)) {
			return new LogResult(fromLineNum, 0, "readLog fail, log identifier not found", true);
		}

		ConcurrentLinkedQueue<String> lines = logCache.get(logFileName);
		if (lines == null || lines.isEmpty()) {
			return new LogResult(fromLineNum, 0, "readLog fail, log not exists in cache", true);
		}

		// read data
		StringBuilder logContentBuilder = new StringBuilder();
		int currentLineNum = 0;
		int toLineNum = 0;

		for (String line : lines) {
			currentLineNum++;

			if (currentLineNum < fromLineNum) {
				continue;
			}

			toLineNum = currentLineNum;
			logContentBuilder.append(line).append(System.lineSeparator());
		}

		// result
		return new LogResult(fromLineNum, toLineNum, logContentBuilder.toString(), false);
	}

}
