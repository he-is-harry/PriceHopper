package ca.harryhe.pricehopper.model;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;

@Entity
@Table(name = "products", uniqueConstraints = { @UniqueConstraint(columnNames = { "product_id" }) })
public class Product {
	@Id
	@GeneratedValue (strategy = GenerationType.IDENTITY)
	@Column(name = "product_id", nullable = false, unique = true)
	private int productId;
	@Column(nullable = false, length = 512)
	private String name;
	@Column(nullable = false)
	private BigDecimal price;
	@Column(name = "scientific_price")
	private BigDecimal scientificPrice;
	@Column(name = "sci_unit_amount")
	private Double sciUnitAmount;
	@Column(name = "sci_unit", length = 16)
	private String sciUnit;
	@Column(nullable = false, length = 64)
	private String company;
	@Column(nullable = false, length = 2048)
	private String url;
	@Column(length = 2048)
	private String image;
	
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
	public double getSciUnitAmount() {
		return sciUnitAmount;
	}
	public void setSciUnitAmount(double sciUnitAmount) {
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
}
