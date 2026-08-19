plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.example.visiondemo"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.example.visiondemo"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }


    // —— IMPORTANT ——
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }

    // (opțional, recomandat) toolchain
    kotlin {
        jvmToolchain(17) // This also helps ensure Kotlin uses JDK 17
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = rootProject.extra["kotlinJvmTarget"] as String
    }
}

dependencies {
    // Define versions in libs.versions.toml or at the top of the script
    val cameraxVersion = "1.3.3" // Or reference from libs.versions.toml

    // Camera
    implementation("androidx.camera:camera-core:$cameraxVersion")
    implementation("androidx.camera:camera-camera2:$cameraxVersion")
    implementation("androidx.camera:camera-lifecycle:$cameraxVersion")
    implementation("androidx.camera:camera-view:$cameraxVersion")

    // ML Kit – Face Detection (pentru ROI față)
    implementation("com.google.mlkit:face-detection:16.1.6")

    // MediaPipe Tasks – Hand Landmarker (21 landmark-uri / mână)
    implementation("com.google.mediapipe:tasks-vision:0.10.26")
    implementation("com.google.mediapipe:tasks-core:0.10.26")

    // TensorFlow Lite – rulăm modelele tflite
    implementation("org.tensorflow:tensorflow-lite:2.14.0")
    implementation("org.tensorflow:tensorflow-lite-gpu:2.14.0") // (opțional) delegate GPU/NNAPI
    implementation("org.tensorflow:tensorflow-lite-task-vision:0.4.4")  // util pt. pre/post proc generic

    implementation("com.google.android.material:material:1.12.0")
}