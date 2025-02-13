package com.culebra

import com.intellij.lang.Language

class CulebraLanguage private constructor() : Language("Culebra") {
    companion object {
        @JvmStatic
        val INSTANCE = CulebraLanguage()
    }
}
