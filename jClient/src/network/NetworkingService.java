package network;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class NetworkingService implements OmgUbuntuApi{

	@Override
	public String loadPosts() {
		String result = "";
		
		try {
			URL baseUrl = new URL("http://213.165.91.3/api/posts");
			URLConnection conn = baseUrl.openConnection();
			BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			String inLine;
			while((inLine = in.readLine()) != null) {
				result += inLine;
			}
			in.close();
		} catch(IOException e) {
			
		}
		
		return result;
	}

}
