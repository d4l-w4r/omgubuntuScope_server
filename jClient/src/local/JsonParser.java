package local;

import com.google.gson.Gson;
import data.VOResponse;

public class JsonParser {
	private final Gson g;
	private VOResponse parsedResponse;
	
	public JsonParser() {
		g =  new Gson();
	}
	
	public VOResponse parseJsonFromString(String input) {
		String[] parts = input.split("\"\\[\\{");
		String cleanedString = parts[0] + new com.google.gson.JsonParser().parse(input).getAsJsonObject().get("content").getAsString();
		parsedResponse = g.fromJson(cleanedString, VOResponse.class);
		return parsedResponse;
	}
}
