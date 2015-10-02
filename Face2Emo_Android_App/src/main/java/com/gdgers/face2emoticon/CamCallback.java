package com.gdgers.face2emoticon;

import android.hardware.Camera;
import android.util.Log;

public class CamCallback implements Camera.PreviewCallback{
    public void onPreviewFrame(byte[] data, Camera camera){
        // Process the camera data here
        Log.d("Send byte[] to server", "do it");
    }
}
