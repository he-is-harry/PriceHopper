package ca.harryhe.pricehopper.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import ca.harryhe.pricehopper.model.Category;
import ca.harryhe.pricehopper.model.view.CategoryResult;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

@Service
public class SearchService {
	
	@PersistenceContext
	private EntityManager em;
	
	public List<CategoryResult> getHomeData() {
		List<Category> homeCategories = em.createQuery("SELECT pc.category FROM PageCategory pc"
													 + " WHERE pc.appPage.pageName = 'Home'"
												     + " ORDER BY pc.sortOrder ASC", Category.class).getResultList();
		
		List<CategoryResult> homeCategoriesResult = new ArrayList<>();
		for(Category category: homeCategories) {
			homeCategoriesResult.add(new CategoryResult(category));
		}
		
		return homeCategoriesResult;
	}
	
	public List<CategoryResult> getRecommendedCategories() {
		List<Category> recommendedCategories = em.createQuery("SELECT pc.category FROM PageCategory pc WHERE pc.appPage.pageName = 'Recommended'"
															+ " ORDER BY pc.sortOrder ASC", Category.class).getResultList();
		List<CategoryResult> recommendedCategoriesResult = new ArrayList<>();
		for(Category category: recommendedCategories) {
			recommendedCategoriesResult.add(new CategoryResult(category));
		}
		return recommendedCategoriesResult;
	}
}
