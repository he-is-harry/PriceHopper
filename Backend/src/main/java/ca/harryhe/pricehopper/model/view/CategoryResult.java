package ca.harryhe.pricehopper.model.view;

import java.util.ArrayList;
import java.util.List;

import ca.harryhe.pricehopper.model.Category;
import ca.harryhe.pricehopper.model.Product;

public class CategoryResult {
	public String categoryName;
	public String categoryImage;
	public List<ProductResult> products;
	
	public CategoryResult(Category category) {
		this.categoryName = category.getCategoryName();
		this.categoryImage = category.getCategoryImage();
		this.products = new ArrayList<>();
		for(Product product: category.getProducts()) {
			products.add(new ProductResult(product));
		}
	}
}
