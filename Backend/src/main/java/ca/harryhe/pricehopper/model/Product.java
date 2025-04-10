package ca.harryhe.pricehopper.model;

import java.math.BigDecimal;

import org.hibernate.annotations.Type;

import ca.harryhe.pricehopper.dto.ProductSearchDTO;
import io.hypersistence.utils.hibernate.type.search.PostgreSQLTSVectorType;
import jakarta.persistence.Column;
import jakarta.persistence.ColumnResult;
import jakarta.persistence.ConstructorResult;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Index;
import jakarta.persistence.NamedNativeQuery;
import jakarta.persistence.SqlResultSetMapping;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;

@Entity
@Table(name = "products", uniqueConstraints = { @UniqueConstraint(columnNames = { "product_id" }) }, indexes = {
		@Index(name = "products_search_vector_idx", columnList = "search_vector") })
@SqlResultSetMapping(
    name = "ProductSearchMapping",
    classes = @ConstructorResult(
        targetClass = ProductSearchDTO.class,
        columns = {
            @ColumnResult(name = "product_id", type = int.class),
            @ColumnResult(name = "name", type = String.class),
            @ColumnResult(name = "price", type = BigDecimal.class),
            @ColumnResult(name = "scientific_price", type = BigDecimal.class),
            @ColumnResult(name = "sci_unit_amount", type = Double.class),
            @ColumnResult(name = "sci_unit", type = String.class),
            @ColumnResult(name = "company", type = String.class),
            @ColumnResult(name = "url", type = String.class),
            @ColumnResult(name = "image", type = String.class),
            @ColumnResult(name = "rank", type = double.class)
        }
    )
)
// Native Search Query
@NamedNativeQuery(name = "searchProductsByName", resultClass = ProductSearchDTO.class,
	resultSetMapping = "ProductSearchMapping",
	query = "SELECT p.*, ts_rank_cd(search_vector, query) AS rank"
		 + " FROM products p, to_tsquery('english', :parsedSearch) query"
		 + " WHERE search_vector @@ query"
		 + " ORDER BY rank DESC"
		 + " LIMIT :limit")

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
	@Type(PostgreSQLTSVectorType.class)
	@Column(name = "search_vector", columnDefinition = "tsvector")
	private String searchVector;
	
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
