package com.culebra

import com.intellij.openapi.fileTypes.LanguageFileType
import com.intellij.openapi.util.IconLoader
import javax.swing.Icon

class CulebraFileType private constructor() : LanguageFileType(CulebraLanguage.INSTANCE) {
    companion object {
        @JvmStatic
        val INSTANCE = CulebraFileType()
    }

    override fun getName() = "Culebra"
    override fun getDescription() = "Culebra language file"
    override fun getDefaultExtension() = "culebra"
    override fun getIcon(): Icon? = null // TODO: Add icon later if needed
}
