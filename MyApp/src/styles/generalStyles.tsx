import { StyleSheet, Dimensions } from 'react-native';

const screenWidth = Dimensions.get('window').width;
const itemCardWidth = screenWidth * 0.4;
const globalStyles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#F5F4F2',
  },

  scrollContent: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    paddingHorizontal: 15,
    paddingTop: 60,
    alignItems: 'center',
    gap: 10, // Added space between items
  },

  screen: {
    flex: 1,
    backgroundColor: '#F5F4F2',
    //paddingBottom: 100, 
  },

  titleContainer: {
    width: '100%',
    alignItems: 'center',
    marginTop: 80,
    marginBottom: 30,
  },

  title: {
    fontSize: 26,
    fontWeight: '600',
    color: '#2C2C2C',
    fontFamily: 'System',
    textAlign: 'center'
  },

  subtitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#4B3869',
  },

  input: {
    width: '100%',
    height: 50,
    borderWidth: 1,
    borderColor: '#E0DED9',
    borderRadius: 10,
    paddingHorizontal: 12,
    marginBottom: 15,
    backgroundColor: '#FFFFFF',
    fontSize: 16,
  },

  buttonContainer: {
    width: '100%',
    marginTop: 10,
  },

  button: {
    flexDirection: 'row',
    backgroundColor: '#EDE9E3',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
  },

  buttonText: {
    color: '#4A3F35',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },

  miniIconButton: {
    padding: 10,
    borderRadius: 50,
    backgroundColor: '#EDE9E3',
    alignItems: 'center',
    justifyContent: 'center',
  },

  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    marginBottom: 20,
    width: '48%',
    overflow: 'hidden',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },

  image: {
    width: '100%',
    height: 220,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },

  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#2C2C2C',
    paddingVertical: 8,
    paddingHorizontal: 10,
  },

  link: {
    marginTop: 20,
    color: '#6A5D4D',
    fontSize: 16,
    textDecorationLine: 'underline',
  },

  registerScreen: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#F5F4F2',
  },

  registerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#2C2C2C',
  },

  instruction: {
    fontSize: 18,
    marginBottom: 20,
    textAlign: 'center',
    color: '#2C2C2C',
  },

  error: {
    color: 'red',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 20,
  },

  searchScreen: {
    flex: 1,
    backgroundColor: '#F5F4F2',
    padding: 20,
    paddingTop: 60,
  },

  formGroup: {
    width: '100%',
    alignItems: 'center',
    gap: 12,
  },

  // item view styling
  itemCard: {
    width: itemCardWidth,
    borderRadius: 10,
    overflow: 'hidden',
    backgroundColor: '#fff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    marginBottom: 10,
    marginRight: 15,
    marginTop: 10,
  },

  itemImage: {
    width: '100%',
    height: 160,
    borderTopLeftRadius: 10,
    borderTopRightRadius: 10,
  },

  itemDetails: {
    height: 60,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 6,
    backgroundColor: '#F8F4FF',
    borderBottomLeftRadius: 10,
    borderBottomRightRadius: 10,
  },

  // Added horizontal category scroll
  categoryScroll: {
    paddingVertical: 10,
  },

  categoryContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },

  categoryButton: {
    backgroundColor: '#4B3869',
    borderRadius: 25,
    paddingVertical: 10,
    paddingHorizontal: 20,
    marginRight: 15,
  },

  categoryText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '500',
  },

  // Clothing Detail specific styles
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 40,
  },

  imageWrapper: {
    width: 300,
    height: 300,
    borderRadius: 12,
    overflow: 'hidden',
    alignSelf: 'center',
  },

  itemInfo: {
    paddingHorizontal: 20,
    paddingTop: 20,
  },

  itemTitle: {
    fontSize: 24,
    marginBottom: 8,
  },

  itemDescription: {
    lineHeight: 20,
  },

  favouriteButtonContainer: {
    paddingHorizontal: 20,
    marginBottom: 40,
  },
});

export default globalStyles;
