package data;

import java.util.List;
import java.util.Map;


public class VOResponse {
	private String responseCode;
	private Map<String, List<VOContent>> content;

	public String getResponseCode() {
		return responseCode;
	}

	public void setResponseCode(String responseCode) {
		this.responseCode = responseCode;
	}

	public Map<String, List<VOContent>> getContent() {
		return content;
	}

	public void setContent(Map<String, List<VOContent>> content) {
		this.content = content;
	}
}
