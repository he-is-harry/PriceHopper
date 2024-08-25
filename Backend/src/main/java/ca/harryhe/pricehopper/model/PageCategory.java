package ca.harryhe.pricehopper.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;

@Entity
@Table(name = "page_categories", uniqueConstraints = { @UniqueConstraint(columnNames = { "page_category_id" }) })
public class PageCategory {
	@Id
	@GeneratedValue (strategy = GenerationType.IDENTITY)
	@Column(name = "page_category_id", nullable = false, unique = true)
	private int pageCategoryId;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "app_page_id", nullable = false)
	private AppPage appPage;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "category_id", nullable = false)
	private Category category;
	
	@Column(name = "sort_order")
	private Integer sortOrder;
}
