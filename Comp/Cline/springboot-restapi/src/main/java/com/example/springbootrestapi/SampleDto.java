package com.example.springbootrestapi;

public class SampleDto {
    private String result;

    public SampleDto() {}
    public SampleDto(String result) {
        this.result = result;
    }
    public String getResult() {
        return result;
    }
    public void setResult(String result) {
        this.result = result;
    }
}
