package ca.harryhe.pricehopper.dto;

import java.math.BigDecimal;
import java.text.DecimalFormat;
import java.text.NumberFormat;

import ca.harryhe.pricehopper.model.Product;

public class ProductResult {
	public int productId;
	public String name;
	public BigDecimal price;
	public String sciPrice;
	public String company;
	public String url;
	public String image;
	
	public ProductResult(Product product) {
		this.productId = product.getProductId();
		this.name = product.getName();
		this.price = product.getPrice();
		
		if (product.getScientificPrice() != null) {
			String sciPrice = NumberFormat.getCurrencyInstance().format(product.getScientificPrice()) + " / ";
			if (product.getSciUnitAmount() != 1) {
				DecimalFormat df = new DecimalFormat("#.00"); 
				sciPrice += df.format(product.getSciUnitAmount());
			}
			sciPrice += product.getSciUnit();
			this.sciPrice = sciPrice;
		}
		
		
		this.company = product.getCompany();
		this.url = product.getUrl();
		this.image = product.getImage();
	}
	
	public ProductResult(ProductSearchDTO product) {
		this.productId = product.getProductId();
		this.name = product.getName();
		this.price = product.getPrice();
		
		if (product.getScientificPrice() != null) {
			String sciPrice = NumberFormat.getCurrencyInstance().format(product.getScientificPrice()) + " / ";
			if (product.getSciUnitAmount() != 1) {
				DecimalFormat df = new DecimalFormat("#.00"); 
				sciPrice += df.format(product.getSciUnitAmount());
			}
			sciPrice += product.getSciUnit();
			this.sciPrice = sciPrice;
		}
		
		this.company = product.getCompany();
		this.url = product.getUrl();
		this.image = product.getImage();
	}
}
