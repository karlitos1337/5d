package com.xxl.job.core.thread;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * job log clean thread - disabled for console logging mode
 *
 * @author xuxueli 2017-12-29 16:23:43
 */
public class JobLogFileCleanThread {
    private static Logger logger = LoggerFactory.getLogger(JobLogFileCleanThread.class);

    private static JobLogFileCleanThread instance = new JobLogFileCleanThread();

    public static JobLogFileCleanThread getInstance() {
        return instance;
    }

    public void start(final long logRetentionDays) {
        logger.info("Console logging mode: log file cleanup is disabled");
    }

    public void toStop() {
        logger.info("Console logging mode: log file cleanup thread stop requested (no-op)");
    }

}
