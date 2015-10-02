package com.gdgers.face2emoticon;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.hardware.Camera;
import android.util.Log;
import android.widget.FrameLayout;

public class CamCaptureService extends Service {
    public CamCaptureService() {
    }

    @Override
    public void onCreate(){
        // Setup the camera and the preview object
        Camera mCamera = Camera.open(0);
        CamPreview camPreview = new CamPreview(this,mCamera);
        camPreview.setSurfaceTextureListener(camPreview);

    // Connect the preview object to a FrameLayout in your UI
    // You'll have to create a FrameLayout object in your UI to place this preview in
        //FrameLayout preview = (FrameLayout) findViewById(R.id.cameraView);
        //preview.addView(camPreview);
        Log.d("CamCaptureService", "Waiting for Callback");
    // Attach a callback for preview
        CamCallback camCallback = new CamCallback();
        mCamera.setPreviewCallback(camCallback);
    }
    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
