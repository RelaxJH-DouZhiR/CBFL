
//===========================================================================
//
//  This program use Eclipse JDT to parse java source files
//  and dumps resulting AST in JSON representation.
//
//---------------------------------------------------------------------------
//
//  Copyright (C) 2015
//  by Oleg Mazko(o.mazko@mail.ru).
//
//  The author gives unlimited permission to copy and distribute
//  this file, with or without modifications, as long as this notice
//  is preserved, and any changes are properly documented.
//

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.io.*;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.eclipse.jdt.core.JavaCore;
import org.eclipse.jdt.core.compiler.IProblem;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.ASTVisitor;
import org.eclipse.jdt.core.dom.Comment;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.dom.Expression;
import org.eclipse.jdt.core.dom.InfixExpression;

public class App {
	static String readFile(final String path, final Charset encoding) throws IOException {
		final byte[] encoded = Files.readAllBytes(Paths.get(path));
		return new String(encoded, encoding);
	}

	public static void main(final String[] args) throws Exception {
		String FATHER_PATH2 = "E:/";
		String project = "mockito";
		for (int version = 1; version <= 38; version++) {
			if (version != 9999) {
				File ASTPath = new File("C:/ssdcode/CBFL/dataset/" + project + "/ASTpath/" + project + "-"
						+ String.valueOf(version) + ".txt");

				FileReader ASTFileReader = new FileReader(ASTPath);
				BufferedReader ASTBufReader = new BufferedReader(ASTFileReader);
				String javaCodePath;
				while ((javaCodePath = ASTBufReader.readLine()) != null) {
					javaCodePath = FATHER_PATH2 + javaCodePath;
					if (javaCodePath.length() > 0) {
						ByteArrayOutputStream baoStream = new ByteArrayOutputStream(1024);
						PrintStream cacheStream = new PrintStream(baoStream);
						PrintStream oldStream = System.out;
						System.setOut(cacheStream);
						ast(javaCodePath + ".java", "h");
						String message = baoStream.toString();
						System.setOut(oldStream);
						BufferedWriter out = new BufferedWriter(new FileWriter(javaCodePath + ".json"));
						out.write(message);
						out.close();
						System.out.println(project + " " + String.valueOf(version) + " " + javaCodePath + " -> ok");
					}
				}
				ASTFileReader.close();
				ASTBufReader.close();

			}
		}
	}

	private static void ast(final String file, final String cmd) throws IOException {
		@SuppressWarnings("deprecation")
		final ASTParser parser = ASTParser.newParser(AST.JLS4); // JLS4 (aka
																// JLS7)
		final String src = readFile(file, StandardCharsets.UTF_8);
		parser.setSource(src.toCharArray());
		parser.setKind(ASTParser.K_COMPILATION_UNIT);
		final Map<?, ?> options = JavaCore.getOptions();
		JavaCore.setComplianceOptions(JavaCore.VERSION_1_7, options);
		parser.setCompilerOptions(options);
		final CompilationUnit cu = (CompilationUnit) parser.createAST(null);
		for (IProblem problem : cu.getProblems()) {
			System.err.println(problem);
		}
		cu.accept(new ASTVisitor() {
			// Eclipse AST optimize deeply nested expressions of the form L op R
			// op R2
			// op R3... where the same operator appears between
			// all the operands. This
			// function disable such optimization back to tree view.
			@Override
			public boolean visit(final InfixExpression node) {
				if (node.hasExtendedOperands()) {
					@SuppressWarnings("unchecked")
					List<Expression> operands = new ArrayList<>(node.extendedOperands());
					Collections.reverse(operands);
					operands.add(node.getRightOperand());
					final Expression firstOperand = operands.remove(0);
					firstOperand.delete(); // remove node from its parent
					node.setRightOperand(firstOperand);
					InfixExpression last = node;
					for (final Expression expr : operands) {
						InfixExpression infixExpression = node.getAST().newInfixExpression();
						infixExpression.setOperator(node.getOperator());
						expr.delete();
						infixExpression.setRightOperand(expr);
						final Expression left = last.getLeftOperand();
						last.setLeftOperand(infixExpression);
						infixExpression.setLeftOperand(left);
						last = infixExpression;
					}
				}

				return super.visit(node);
			}
		});

		if (cmd.equals("c")) {
			try (final UglyMathCommentsExtractor cex = new UglyMathCommentsExtractor(cu, src)) {
				final ASTDumper dumper = new ASTDumper(cex);
				dumper.dump(cu, cu);
				System.out.flush();
			}
		} else {
			final ASTDumper dumper = new ASTDumper();
			for (final Object comment : cu.getCommentList()) {
				((Comment) comment).delete();
			}
			dumper.dump(cu, cu);
		}
	}
}
