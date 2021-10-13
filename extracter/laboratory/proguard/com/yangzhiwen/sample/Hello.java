package com.yangzhiwen.sample;

public class Hello {
    public String data;

    /**
    -keep class com.yangzhiwen.sample.Hello { *; }
    private String data2; // 不被混淆
    private void track(String text) { } // 不被混淆

    -keep class com.yangzhiwen.sample.Hello {
        !private <fields>;
        !private <methods>;
    }
    private String data2; // 被混淆
    private void track(String text) { } // 被混淆
     */
    private String data2;

    public void set(String text) {
        track("set " + text);
        this.data2 = text;
    }

    public String say() {
        track("say " + this.data2);
        return this.data2;
    }

    private void track(String text) {
        this.data = text;
        System.out.println("track the " + text);
    }
}