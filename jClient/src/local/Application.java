package local;

import data.VOContent;
import data.VOResponse;
import network.NetworkingService;

public class Application {
	
	public static void main(String[] args) {
		final NetworkingService netService = new NetworkingService();
		
		new Thread(new Runnable() {
			
			@Override
			public void run() {
				String jsonString = netService.loadPosts();
				if (jsonString != null) {
					parseResult(jsonString);
				}
			}
		}).start();
	}
	
	public static void parseResult(String queryResult) {
		VOResponse response = new JsonParser().parseJsonFromString(queryResult);
		System.out.println(response.getResponseCode());
		for (VOContent object : response.getContent()) {
			System.out.println(object.toString());
		}
	}
	
}
