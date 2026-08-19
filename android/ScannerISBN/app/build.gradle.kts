plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)

}

android {
    namespace = "aplicatie.isbn"
    compileSdk = 36

    defaultConfig {
        applicationId = "aplicatie.isbn"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
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
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
}

// In your app/build.gradle.kts file

dependencies {

    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.activity)
    implementation(libs.androidx.constraintlayout)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)

    // CameraX
    val cameraxVersion = "1.3.3" // Changed from def to val
    implementation("androidx.camera:camera-core:$cameraxVersion") // Corrected string interpolation
    implementation("androidx.camera:camera-camera2:$cameraxVersion") // Corrected string interpolation
    implementation("androidx.camera:camera-lifecycle:$cameraxVersion") // Corrected string interpolation
    implementation("androidx.camera:camera-view:$cameraxVersion") // PreviewView, Corrected string interpolation

    // ML Kit: Barcode + Text
    implementation("com.google.mlkit:barcode-scanning:17.2.0")
    implementation("com.google.mlkit:text-recognition:16.0.0")

    // Retrofit (Google Books API)
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-moshi:2.11.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
}
