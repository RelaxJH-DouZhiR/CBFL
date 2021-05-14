/*
 * @Author: your name
 * @Date: 2021-05-14 11:53:21
 * @LastEditTime: 2021-05-14 16:38:47
 * @Description: file content
 */
package com.example;

import com.github.javaparser.JavaParser;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.visitor.ModifierVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.resolution.types.ResolvedType;
import com.github.javaparser.symbolsolver.*;
import com.github.javaparser.symbolsolver.model.resolution.TypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;

import jdk.internal.org.objectweb.asm.MethodVisitor;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collector;

public class MainMethodAccess {
    private static final String FILE_PATH = "/Users/lvlaxjh/code/CBFL/AST/demo/src/main/java/com/example/App.java";//文件路径
    public static void main(String[] args) throws Exception {
        TypeSolver typeSolver = new CombinedTypeSolver();
        JavaSymbolSolver symbolSolver = new JavaSymbolSolver(typeSolver);
        StaticJavaParser
                .getConfiguration()
                .setSymbolResolver(symbolSolver);
        CompilationUnit cu = StaticJavaParser.parse(new File(FILE_PATH));
        System.out.println(cu.getClassByName("App"));
        System.out.println(cu);

        // cu.findAll(AssignExpr.class).forEach(ae -> {
        //     ResolvedType resolvedType = ae.calculateResolvedType();
        //     System.out.println(ae.toString() + " is a: " + resolvedType);
        //     });




        // FileInputStream in = new FileInputStream(FILE_PATH);//导入文件
        // // Statement statement = StaticJavaParser.parseStatement("int a = 0;");
        // CompilationUnit cu = StaticJavaParser.parse(in);//生成CompilationUnit树
        // List<String> methodList = new ArrayList<>();
        // new MethodName().visit(cu, methodList);//获取函数名列表
        // System.out.println("method name list -> " + methodList);
        // System.out.println(cu.getAllComments());
        new IntegerLiteralModifier().visit(cu, null);
    }

    private static class IntegerLiteralModifier extends ModifierVisitor<Void> {// 获取函数名列表
        @Override
        public FieldDeclaration visit(FieldDeclaration fd, Void arg) {
            super.visit(fd, arg);
            return fd;
            // ml.add(md.getNameAsString());
            // System.out.println("method name is -> " + md.getName());

        }
    }



    // private static class MethodName extends VoidVisitorAdapter<List<String>> {//获取函数名列表
    //     @Override
    //     public void visit(MethodDeclaration md, List<String> ml) {
    //         super.visit(md, ml);
    //         ml.add(md.getNameAsString());
    //         System.out.println("method name is -> "+md.getName());
    //     }
    // }

}