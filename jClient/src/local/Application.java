package local;

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
		//Do magic, make VO Instances
	}
	
}
