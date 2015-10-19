package local;

import java.util.ArrayList;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import data.VOContent;
import data.VOResponse;

public class JsonParser {
	private final Gson g;
	private VOResponse parsedResponse;
	
	public JsonParser() {
		g =  new Gson();
	}
	
	public VOResponse parseJsonFromString(String input) {
		String testString = "{\"responseCode\":200, \"content\":[{\"title\":\"testTitle\",\"description\":\"abc123\",\"shortDescription\":\"abc\",\"author\":\"daniel\",\"imageUrl\":\"http://foo.bar/img.jpg\",\"ressourceUrl\":\"http://foo.baz\"}]}";
		parsedResponse = g.fromJson(testString, VOResponse.class);
		return parsedResponse;
	}
}
