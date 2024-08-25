package ca.harryhe.pricehopper;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@SpringBootApplication
public class PricehopperApplication {

	public static void main(String[] args) {
		SpringApplication.run(PricehopperApplication.class, args);
	}
	
	@Bean
	public WebMvcConfigurer corsConfigurer() {
		return new WebMvcConfigurer() {
			@Override
			public void addCorsMappings(CorsRegistry registry) {
				// Configure allowed origins to be your client domain
				registry.addMapping("/**").allowedOrigins("http://localhost:8081");
			}
		};
	}

}
