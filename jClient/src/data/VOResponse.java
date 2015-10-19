package data;

import java.util.List;
import java.util.Map;


public class VOResponse {
	private String responseCode;
	private List<VOContent> content;

	public String getResponseCode() {
		return responseCode;
	}

	public void setResponseCode(String responseCode) {
		this.responseCode = responseCode;
	}

	public List<VOContent> getContent() {
		return content;
	}

	public void setContent(List<VOContent> content) {
		this.content = content;
	}
}
