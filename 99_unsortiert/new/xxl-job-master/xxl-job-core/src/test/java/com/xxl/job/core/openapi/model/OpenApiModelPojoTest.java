package com.xxl.job.core.openapi.model;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class OpenApiModelPojoTest {

    @Test
    void callbackRequestConstructorAndToString() {
        CallbackRequest request = new CallbackRequest(1001L, 1700000000000L, 200, "ok");

        assertEquals(1001L, request.getLogId());
        assertEquals(1700000000000L, request.getLogDateTim());
        assertEquals(200, request.getHandleCode());
        assertEquals("ok", request.getHandleMsg());

        String text = request.toString();
        assertTrue(text.contains("HandleCallbackParam"));
        assertTrue(text.contains("logId=1001"));
        assertTrue(text.contains("handleCode=200"));
    }

    @Test
    void idleBeatRequestGetterSetterAndConstructor() {
        IdleBeatRequest request = new IdleBeatRequest(7);
        assertEquals(7, request.getJobId());

        request.setJobId(8);
        assertEquals(8, request.getJobId());
    }

    @Test
    void killRequestGetterSetterAndConstructor() {
        KillRequest request = new KillRequest(11);
        assertEquals(11, request.getJobId());

        request.setJobId(12);
        assertEquals(12, request.getJobId());
    }

    @Test
    void logRequestGetterSetterAndConstructor() {
        LogRequest request = new LogRequest(1700000000001L, 22L, 3);

        assertEquals(1700000000001L, request.getLogDateTim());
        assertEquals(22L, request.getLogId());
        assertEquals(3, request.getFromLineNum());

        request.setFromLineNum(9);
        assertEquals(9, request.getFromLineNum());
    }

    @Test
    void logResultGetterSetterAndConstructor() {
        LogResult result = new LogResult(1, 5, "line", false);

        assertEquals(1, result.getFromLineNum());
        assertEquals(5, result.getToLineNum());
        assertEquals("line", result.getLogContent());
        assertTrue(!result.isEnd());

        result.setEnd(true);
        assertTrue(result.isEnd());
    }

    @Test
    void registryRequestConstructorAndToString() {
        RegistryRequest request = new RegistryRequest("EXECUTOR", "key-a", "addr");

        assertEquals("EXECUTOR", request.getRegistryGroup());
        assertEquals("key-a", request.getRegistryKey());
        assertEquals("addr", request.getRegistryValue());

        String text = request.toString();
        assertTrue(text.contains("RegistryParam"));
        assertTrue(text.contains("registryKey='key-a'"));
    }

    @Test
    void triggerRequestGetterSetterAndToString() {
        TriggerRequest request = new TriggerRequest();
        request.setJobId(9);
        request.setExecutorHandler("handler");
        request.setExecutorParams("a=1");
        request.setExecutorBlockStrategy("SERIAL_EXECUTION");
        request.setExecutorTimeout(120);
        request.setLogId(99L);
        request.setLogDateTime(1700000000002L);
        request.setGlueType("GLUE_GROOVY");
        request.setGlueSource("println(1)");
        request.setGlueUpdatetime(1700000000003L);
        request.setBroadcastIndex(1);
        request.setBroadcastTotal(3);

        assertEquals(9, request.getJobId());
        assertEquals("handler", request.getExecutorHandler());
        assertEquals("a=1", request.getExecutorParams());
        assertEquals("SERIAL_EXECUTION", request.getExecutorBlockStrategy());
        assertEquals(120, request.getExecutorTimeout());
        assertEquals(99L, request.getLogId());
        assertEquals(1700000000002L, request.getLogDateTime());
        assertEquals("GLUE_GROOVY", request.getGlueType());
        assertEquals("println(1)", request.getGlueSource());
        assertEquals(1700000000003L, request.getGlueUpdatetime());
        assertEquals(1, request.getBroadcastIndex());
        assertEquals(3, request.getBroadcastTotal());

        String text = request.toString();
        assertTrue(text.contains("TriggerParam"));
        assertTrue(text.contains("jobId=9"));
        assertTrue(text.contains("broadcastTotal=3"));
    }
}
