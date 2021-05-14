/*
 * @Author: your name
 * @Date: 2021-05-14 11:45:42
 * @LastEditTime: 2021-05-14 15:19:55
 * @Description: file content
 */
package com.example;

/**
 * Hello world!
 */
public final class App {
    private App() {
    }

    /**
     * Says hello to the world.
     * @param args The arguments of the program.
     */
    public static void main(String[] args) {
        Integer testNumber = 30;
        if (testNumber < 50) {
            System.out.println(testNumber);
        } else {
            System.out.println(">50");
        }
        for (int i = 0; i < 5; i++) {
            System.out.println(i);
        }
    }
    
    public Integer getSum(Integer a,Integer b) {
        Integer c = a + b;//求和
        return c;
    }
}
