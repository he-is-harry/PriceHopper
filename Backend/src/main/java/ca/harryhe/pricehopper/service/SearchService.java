package ca.harryhe.pricehopper.service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import ca.harryhe.pricehopper.dto.BasicCategoryResult;
import ca.harryhe.pricehopper.dto.CategoryResult;
import ca.harryhe.pricehopper.dto.CategorySearchDTO;
import ca.harryhe.pricehopper.dto.ProductResult;
import ca.harryhe.pricehopper.dto.ProductSearchDTO;
import ca.harryhe.pricehopper.model.Category;
import ca.harryhe.pricehopper.model.Product;
import ca.harryhe.pricehopper.repository.CategoryRepository;
import ca.harryhe.pricehopper.repository.ProductRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

@Service
public class SearchService {
	
	@PersistenceContext
	private EntityManager em;
	
	@Autowired
	private CategoryRepository categoryRepository;
	
	@Autowired
	private ProductRepository productRepository;
	
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
	
	public List<BasicCategoryResult> getRelevantCategories(String search) {
		// Parse search into unique words
		String [] words = search.trim().toLowerCase().split("\\s+");
		Set<String> wordSet = new HashSet<String>(Arrays.asList(words));
		String[] uniqueWords = wordSet.toArray(new String[wordSet.size()]);
		
		String query = "%" + String.join("%", uniqueWords) + "%";
		
		List<Category> unrankedCategories = categoryRepository.searchCategoriesByName(query);
		
		// Find the number of unique words that match and the first index where a word matches
		List<CategorySearchDTO> categoryDetails = new ArrayList<>();
		for(Category category: unrankedCategories) {
			int numMatchingWords = 0;
			int firstMatchingIndex = category.getCategoryName().length();
			for (String word: uniqueWords) {
				int index = category.getCategoryName().toLowerCase().indexOf(word.toLowerCase());
				if (index >= 0) {
					numMatchingWords++;
					if (index < firstMatchingIndex) {
						firstMatchingIndex = index;
					}
				}
			}
			
			categoryDetails.add(new CategorySearchDTO(category, numMatchingWords, firstMatchingIndex));
		}
		
		// Rank the categories first by number of matching words then first index
		Collections.sort(categoryDetails);
		
		List<BasicCategoryResult> categoryResults = new ArrayList<>();
		for (CategorySearchDTO category: categoryDetails) {
			categoryResults.add(new BasicCategoryResult(category));
		}
		return categoryResults;
	}
	
	public List<ProductResult> search(String search, Integer categoryId, Integer limit) {
		
		if (search == null || search.isBlank()) {
			// Get all products within the category
			Category category = categoryRepository.findCategoryById(categoryId);
			
			List<Product> searchProducts;
			if (category == null) {
				searchProducts = new ArrayList<>();
			} else {
				searchProducts = category.getProducts();
			}
			
			List<ProductResult> searchProductsResult = new ArrayList<>();
			for (int i = 0; i < limit && i < searchProducts.size(); i++) {
				searchProductsResult.add(new ProductResult(searchProducts.get(i)));
			}
			return searchProductsResult;
		} else {
			// Create full text search query, with or operators between words
			// so that products with any matching words (lexemes) will be considered
			String[] words = search.trim().split("\\s+");
			String query = String.join(" | ", words);
			// Query database with full text search
			List<ProductSearchDTO> searchResults = productRepository.searchProductsByName(query, limit);
					
			List<ProductResult> searchProductsResult = new ArrayList<>();
			for(ProductSearchDTO result: searchResults) {
				searchProductsResult.add(new ProductResult(result));
			}
			
			return searchProductsResult;
		}
		
	}
}
