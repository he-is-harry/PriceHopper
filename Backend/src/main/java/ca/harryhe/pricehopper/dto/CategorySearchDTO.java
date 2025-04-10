package ca.harryhe.pricehopper.dto;

import ca.harryhe.pricehopper.model.Category;

public class CategorySearchDTO implements Comparable<CategorySearchDTO>{
	private int categoryId;
	private String categoryName;
	private String categoryImage;
	// Number of unique matching words
	private int numMatchingWords;
	private int firstMatchingIndex;
	
	public CategorySearchDTO(Category category, int numMatchingWords, int firstMatchingIndex) {
		this.categoryId = category.getCategoryId();
		this.categoryName = category.getCategoryName();
		this.categoryImage = category.getCategoryImage();
		this.numMatchingWords = numMatchingWords;
		this.firstMatchingIndex = firstMatchingIndex;
	}
	
	@Override
	public int compareTo(CategorySearchDTO c) {
		if (this.numMatchingWords != c.numMatchingWords) {
			// First compare by number of unique matching words descending
			return Integer.compare(c.numMatchingWords, this.numMatchingWords);
		} else {
			// Then compare by the first matching index ascending
			return Integer.compare(this.firstMatchingIndex, c.firstMatchingIndex);
		}
	}

	public int getCategoryId() {
		return categoryId;
	}

	public void setCategoryId(int categoryId) {
		this.categoryId = categoryId;
	}

	public String getCategoryName() {
		return categoryName;
	}

	public void setCategoryName(String categoryName) {
		this.categoryName = categoryName;
	}

	public String getCategoryImage() {
		return categoryImage;
	}

	public void setCategoryImage(String categoryImage) {
		this.categoryImage = categoryImage;
	}

	public int getNumMatchingWords() {
		return numMatchingWords;
	}

	public void setNumMatchingWords(int numMatchingWords) {
		this.numMatchingWords = numMatchingWords;
	}

	public int getFirstMatchingIndex() {
		return firstMatchingIndex;
	}

	public void setFirstMatchingIndex(int firstMatchingIndex) {
		this.firstMatchingIndex = firstMatchingIndex;
	}
}
