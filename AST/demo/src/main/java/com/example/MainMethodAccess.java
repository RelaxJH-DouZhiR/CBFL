/*
 * @Author: your name
 * @Date: 2021-05-14 11:53:21
 * @LastEditTime: 2021-05-17 16:38:35
 * @Description: file content
 */
package com.example;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.eclipse.jdt.core.JavaCore;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.ASTNode;
import org.eclipse.jdt.core.dom.ASTVisitor;
//--

import org.eclipse.jdt.core.dom.Statement;//-
import org.eclipse.jdt.core.dom.MethodDeclaration;//函数
import org.eclipse.jdt.core.dom.SimplePropertyDescriptor;
import org.eclipse.jdt.core.dom.TypeDeclaration;//类
import org.eclipse.jdt.core.dom.Assignment;
import org.eclipse.jdt.core.dom.ChildListPropertyDescriptor;
import org.eclipse.jdt.core.dom.ChildPropertyDescriptor;
//--
import org.eclipse.jdt.core.dom.CompilationUnit;

public class MainMethodAccess {

    public static void main(String[] args) {
        // 代码文件读取-start
        String FILE_PATH = "/Users/lvlaxjh/code/CBFL/AST/demo/src/main/java/com/example/App.java";// 文件路径
        byte[] input = null;
        try {
            BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream(FILE_PATH));
            input = new byte[bufferedInputStream.available()];
            bufferedInputStream.read(input);
            bufferedInputStream.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // 代码文件读取-end
        // 生成AST树-start
        ASTParser astParser = ASTParser.newParser(AST.JLS_Latest);
        astParser.setSource(new String(input).toCharArray());
        Map options = JavaCore.getOptions();
        JavaCore.setComplianceOptions(JavaCore.VERSION_1_8, options);
        astParser.setCompilerOptions(options);
        CompilationUnit resultAST = (CompilationUnit) astParser.createAST(null);
        // System.out.println(result);
        // 生成AST树-end
        // AST树访问-start
        DemoVisitor visitor = new DemoVisitor();
        // System.out.println(resultAST.getLineNumber(2));
        // System.out.println(resultAST.getPosition(2, 1));
        System.out.println(resultAST.getAST());
        
        // resultAST.accept(ASTVisitor.visit());
        // AST树访问-end
        print(resultAST);
    }

    static void print(ASTNode node) {
        List properties = node.structuralPropertiesForType();
        for (Iterator iterator = properties.iterator(); iterator.hasNext();) {
            Object descriptor = iterator.next();
            if (descriptor instanceof SimplePropertyDescriptor) {
                SimplePropertyDescriptor simple = (SimplePropertyDescriptor) descriptor;
                Object value = node.getStructuralProperty(simple);
                System.out.println(simple.getId() + " (" + value.toString() + ")");
            } else if (descriptor instanceof ChildPropertyDescriptor) {
                ChildPropertyDescriptor child = (ChildPropertyDescriptor) descriptor;
                ASTNode childNode = (ASTNode) node.getStructuralProperty(child);
                if (childNode != null) {
                    System.out.println("Child (" + child.getId() + ") {");
                    print(childNode);
                    System.out.println("}");
                }
            } else {
                ChildListPropertyDescriptor list = (ChildListPropertyDescriptor) descriptor;
                System.out.println("List (" + list.getId() + "){");
                print((List) node.getStructuralProperty(list));
                System.out.println("}");
            }
        }
    }

    static void print(List nodes) {
        for (Iterator iterator = nodes.iterator(); iterator.hasNext();) {
            print((ASTNode) iterator.next());
        }
    }



    
}






// 重构ASTVisitor-start
class DemoVisitor extends ASTVisitor {
    // 函数-start
    @Override
    public boolean visit(MethodDeclaration node) {
        System.out.println("Method:\t" + node.getName());
        return true;
    }
    // 函数-end

    // 类-srat
    @Override
    public boolean visit(TypeDeclaration node) {
        System.out.println("Class:\t" + node.getName());
        return true;
    }
    // 类-end
    // 类-srat
    @Override
    public boolean visit(Assignment node) {
        System.out.println("Class:\t" + node.toString());
        return true;
    }
    // 类-end
    
}
// 重构ASTVisitor-end
