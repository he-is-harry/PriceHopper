package ca.harryhe.pricehopper.dto;

import java.math.BigDecimal;

public class ProductSearchDTO {
	private int productId;
	private String name;
	private BigDecimal price;
	private BigDecimal scientificPrice;
	private Double sciUnitAmount;
	private String sciUnit;
	private String company;
	private String url;
	private String image;
	// Search relevance rank
	private double rank;
	
	public ProductSearchDTO(int productId, String name, BigDecimal price, BigDecimal scientificPrice,
			Double sciUnitAmount, String sciUnit, String company, String url, String image, double rank) {
		this.productId = productId;
		this.name = name;
		this.price = price;
		this.scientificPrice = scientificPrice;
		this.sciUnitAmount = sciUnitAmount;
		this.sciUnit = sciUnit;
		this.company = company;
		this.url = url;
		this.image = image;
		this.rank = rank;
	}
	
	public int getProductId() {
		return productId;
	}
	public void setProductId(int productId) {
		this.productId = productId;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public BigDecimal getPrice() {
		return price;
	}
	public void setPrice(BigDecimal price) {
		this.price = price;
	}
	public BigDecimal getScientificPrice() {
		return scientificPrice;
	}
	public void setScientificPrice(BigDecimal scientificPrice) {
		this.scientificPrice = scientificPrice;
	}
	public Double getSciUnitAmount() {
		return sciUnitAmount;
	}
	public void setSciUnitAmount(Double sciUnitAmount) {
		this.sciUnitAmount = sciUnitAmount;
	}
	public String getSciUnit() {
		return sciUnit;
	}
	public void setSciUnit(String sciUnit) {
		this.sciUnit = sciUnit;
	}
	public String getCompany() {
		return company;
	}
	public void setCompany(String company) {
		this.company = company;
	}
	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	public String getImage() {
		return image;
	}
	public void setImage(String image) {
		this.image = image;
	}
	public double getRank() {
		return rank;
	}
	public void setRank(double rank) {
		this.rank = rank;
	}
}
