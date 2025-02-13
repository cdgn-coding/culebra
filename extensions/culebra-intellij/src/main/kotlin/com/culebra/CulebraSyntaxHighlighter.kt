package com.culebra

import com.intellij.lexer.Lexer
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors
import com.intellij.openapi.editor.HighlighterColors
import com.intellij.openapi.editor.colors.TextAttributesKey
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase
import com.intellij.psi.TokenType
import com.intellij.psi.tree.IElementType
import com.intellij.lexer.EmptyLexer

class CulebraSyntaxHighlighter : SyntaxHighlighterBase() {
    companion object {
        // Define text attribute keys for different syntax elements
        val KEYWORD = TextAttributesKey.createTextAttributesKey(
            "CULEBRA.KEYWORD",
            DefaultLanguageHighlighterColors.KEYWORD
        )
        val STRING = TextAttributesKey.createTextAttributesKey(
            "CULEBRA.STRING",
            DefaultLanguageHighlighterColors.STRING
        )
        val NUMBER = TextAttributesKey.createTextAttributesKey(
            "CULEBRA.NUMBER",
            DefaultLanguageHighlighterColors.NUMBER
        )
        val COMMENT = TextAttributesKey.createTextAttributesKey(
            "CULEBRA.COMMENT",
            DefaultLanguageHighlighterColors.LINE_COMMENT
        )
        val OPERATOR = TextAttributesKey.createTextAttributesKey(
            "CULEBRA.OPERATOR",
            DefaultLanguageHighlighterColors.OPERATION_SIGN
        )
        val BAD_CHARACTER = TextAttributesKey.createTextAttributesKey(
            "CULEBRA.BAD_CHARACTER",
            HighlighterColors.BAD_CHARACTER
        )

        private val KEYWORDS = setOf(
            "if", "elif", "else", "while", "for", "def",
            "return", "true", "false", "and", "or", "not"
        )

        private val BAD_CHAR_KEYS = arrayOf(BAD_CHARACTER)
        private val KEYWORD_KEYS = arrayOf(KEYWORD)
        private val STRING_KEYS = arrayOf(STRING)
        private val NUMBER_KEYS = arrayOf(NUMBER)
        private val COMMENT_KEYS = arrayOf(COMMENT)
        private val OPERATOR_KEYS = arrayOf(OPERATOR)
        private val EMPTY_KEYS = arrayOf<TextAttributesKey>()
    }

    override fun getHighlightingLexer(): Lexer {
        // TODO: Replace with actual lexer when implemented
        return EmptyLexer()
    }

    override fun getTokenHighlights(tokenType: IElementType): Array<TextAttributesKey> {
        // This is a simplified version. You'll need to implement proper token matching
        return when {
            tokenType == TokenType.BAD_CHARACTER -> BAD_CHAR_KEYS
            tokenType.toString() in KEYWORDS -> KEYWORD_KEYS
            // Add more token type checks when you implement the lexer
            else -> EMPTY_KEYS
        }
    }
}
