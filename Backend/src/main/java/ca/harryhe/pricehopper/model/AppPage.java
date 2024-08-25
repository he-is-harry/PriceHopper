package ca.harryhe.pricehopper.model;

import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;

@Entity
@Table(name = "app_pages", uniqueConstraints = { @UniqueConstraint(columnNames = { "app_page_id" }) })
public class AppPage {
	@Id
	@GeneratedValue (strategy = GenerationType.IDENTITY)
	@Column(name = "app_page_id", nullable = false, unique = true)
	private int appPageId;
	@Column(name = "page_name", nullable = false, length = 64)
	private String pageName;
	
	@OneToMany(fetch = FetchType.LAZY)
	@JoinColumn(name = "app_page_id")
	private List<PageCategory> pageCategories;

	public int getAppPageId() {
		return appPageId;
	}

	public void setAppPageId(int appPageId) {
		this.appPageId = appPageId;
	}

	public String getPageName() {
		return pageName;
	}

	public void setPageName(String pageName) {
		this.pageName = pageName;
	}
	
	public List<PageCategory> getPageCategories() {
		return pageCategories;
	}

	public void setPageCategories(List<PageCategory> pageCategories) {
		this.pageCategories = pageCategories;
	}
}
