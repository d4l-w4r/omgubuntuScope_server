package data;

public class VOContent {
	private String title;
	private String description;
	private String shortDescription;
	private String author;
	private String imageUrl;
	private String ressourceUrl;
	
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public String getShortDescription() {
		return shortDescription;
	}
	public void setShortDescription(String shortDescription) {
		this.shortDescription = shortDescription;
	}
	public String getAuthor() {
		return author;
	}
	public void setAuthor(String author) {
		this.author = author;
	}
	public String getImage() {
		return imageUrl;
	}
	public void setImage(String image) {
		this.imageUrl = image;
	}
	public String getRessourceUrl() {
		return ressourceUrl;
	}
	public void setRessourceUrl(String ressourceUrl) {
		this.ressourceUrl = ressourceUrl;
	}
	
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append("{ title: ").append(title).append(", description: ").append(description).append(", shortDesc: ").append(shortDescription)
		.append(", author: ").append(author).append(", imageUrl: ").append(imageUrl).append(", ressourceUrl: ").append(ressourceUrl).append(" }");
		return sb.toString();
	}
}
