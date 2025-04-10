package ca.harryhe.pricehopper.dto;

public class BasicCategoryResult {
	public int categoryId;
	public String categoryName;
	public String categoryImage;
	
	public BasicCategoryResult(CategorySearchDTO category) {
		this.categoryId = category.getCategoryId();
		this.categoryName = category.getCategoryName();
		this.categoryImage = category.getCategoryImage();
	}
}
