package com.gdgers.face2emoticon;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.ComponentName;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

public class UploadImage extends AsyncTask<byte[], Void, Void> {
    private static InputStream inputStream;
    private static final String SERVER_URL = "http://ec2-52-10-233-195.us-west-2.compute.amazonaws.com:8000/";
    //private static final String SERVER_URL = "http://timberlake.cse.buffalo.edu:8000/";

    private Context context;

    public UploadImage(Context context){
        this.context = context;
    }
    @Override
    protected Void doInBackground(byte[]... params) {
        Log.d("Sending image to server"," " + params.length);
        String image_str = Base64.encodeBytes(params[0]);
        ArrayList<NameValuePair> nameValuePairs = new  ArrayList<NameValuePair>();

        nameValuePairs.add(new BasicNameValuePair("image",image_str));
                try{
                    HttpClient httpclient = new DefaultHttpClient();
                    HttpPost httppost = new HttpPost(SERVER_URL);
                    httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

                    HttpResponse response = httpclient.execute(httppost);
                    //String the_string_response = convertResponseToString(response);
                    String responseStr = EntityUtils.toString(response.getEntity());

                    Log.d("Server Response", responseStr);
                    JSONObject resp = new JSONObject(responseStr);
                    String emo = resp.getString("result");
                    if(emo.equals("F"))
                        StaticGlobals.emojis = "\ud83d\ude12";
                    else if(emo.equals("S"))
                        StaticGlobals.emojis = 	"\ud83d\ude03";
                    else
                        StaticGlobals.emojis = "Uhh, couldn't figure you out ! " + "\ud83d\ude0f";
                    Log.i("Server returns", emo);
                    StaticGlobals.waitingForServer = false;

                }catch(Exception e){
                    Log.e("Error","In uploading file to server" + e.toString());
                }

        return null;
    }

    protected void onPostExecute(String result){

    }

    public static String convertResponseToString(HttpResponse response) throws IllegalStateException, IOException{

        String res = "";
        StringBuffer buffer = new StringBuffer();
        inputStream = response.getEntity().getContent();
        int contentLength = (int) response.getEntity().getContentLength(); //getting content length…..

        if (contentLength < 0){
        }
        else{
            byte[] data = new byte[512];
            int len = 0;
            try
            {
                while (-1 != (len = inputStream.read(data)) )
                {
                    buffer.append(new String(data, 0, len)); //converting to string and appending  to stringbuffer…..
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
            try
            {
                inputStream.close(); // closing the stream…..
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
            res = buffer.toString();     // converting stringbuffer to string…..
        }
        return res;
    }


}
